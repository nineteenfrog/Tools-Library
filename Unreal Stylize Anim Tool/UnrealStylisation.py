import unreal

def stylize_anim(paths, framesToSkip):
	#add to transaction system
	with unreal.ScopedEditorTransaction("Stylize Animation") as trans:
		#loop through all the asset paths
		for path in paths:
			#load asset as level sequence asset
			sequence = unreal.load_asset(path, unreal.LevelSequence)
			try:
				#check if asset is level sequence
				unreal.LevelSequence.cast(sequence)
			except:
				#log error if asset isn't a level sequence and move on to next path
				unreal.log_error("Select at least one sequence asset")
				continue
			#we grab all the tracks of our only binding
			all_tracks = sequence.get_bindings()[0].get_tracks()
			#the track at index 3 contains  the FKControlRig that has all the skeletal animation
			track = all_tracks[3]
			#loop through the sections of the track (the joint)
			for section in track.get_sections():
				#loop through the channels of each section (eg. x rotation)
				for channel in section.get_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
					stylize_channel(channel, framesToSkip)

def stylize_selected_channels(framesToSkip):
	sl = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_channels()
	for channelProxy in sl:  #similar to the logic in bake_selected_channels
		section = channelProxy.section #we loop through all the channels
		channels = section.get_all_channels()
		with unreal.ScopedEditorTransaction("Stylize Animation") as trans:
			for channel in channels:
				if channel.channel_name == channelProxy.channel_name:
					stylize_channel(channel,framesToSkip) #we apply the stylization operation to the channels

def stylize_channel(channel, framesToSkip):
	keys = channel.get_keys()
	key_value = 0
	#loop through all the keys
	for i in range(len(keys)):
		mod_op = i % framesToSkip
		#these are the frames we keep and copy over
		if mod_op == 0:
			key_value = keys[i].get_value()
		#these are the in-betweens, they are deleted unless its the last one
		else:
			#in that case we copy the key from earlier
			if mod_op == (framesToSkip - 1):
				keys[i].set_value(key_value)
			else:
				channel.remove_key(keys[i])

def bake_selected_channels():
	sl = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_channels()
	for channelProxy in sl: #the above function gives a channelProxy object type
		section = channelProxy.section  #we need a MovieSceneScriptingChannel
		channels = section.get_all_channels()
		with unreal.ScopedEditorTransaction("Stylize Animation") as trans: #begin transaction
			for channel in channels:
				if channel.channel_name == channelProxy.channel_name:
					keys = channel.get_keys()
					#the code below does a simple slope calculation with x being the frame number
					#and y being the channel value. This only works between a range of two keys
					y1 = keys[0].get_value()
					x1 = keys[0].get_time().frame_number.value
					y2 = keys[len(keys) - 1].get_value()
					x2 = keys[len(keys) - 1].get_time().frame_number.value
					rate_of_change = (y1 - y2) / (x1 - x2)
					for i in range(0, x2 + 1): #a key is added with the slope at the given frame number
						channel.add_key(unreal.FrameNumber(i), rate_of_change * i, 0.0, unreal.MovieSceneTimeUnit.DISPLAY_RATE,unreal.MovieSceneKeyInterpolation.LINEAR)
