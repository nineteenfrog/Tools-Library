<h1>Final Project Writeup</h1>
Alfredo Fonseca Siqueiros<br>
MSc Technical Art and VFX<br>
Realtime Tool and Pipeline Development<br>
Demo Video: https://youtu.be/zGXWBOulObw<br>
<h2>Background:</h2>
In the last couple of years there has been a shake up  in the animation industry relating to stylistic choices. We can now reach a lot of visual fidelity in computer generated content but it sometimes seems boring to always look at the same style. With the success of movies like The Mitchells vs. the Machines, Spider-Man into the Spider-Verse, and most recently K-Pop Demon Hunters, we could notice a pattern where people are more attracted to stylization rather than realism. One of the ways in which this is achieved is by switching up some of the traditional animation methods.<br>
<img width="975" height="527" alt="image" src="https://github.com/user-attachments/assets/95c3df2e-e8fc-4e6f-af70-b3c676a48fc8" />
<h2>Animating in Twos, Threes, Fours</h2>
One of the techniques I wanted to explore with my tool in order to support my film project is animating in twos. Normally, animation clips are animated in the same framerate that the movie comes in. For example, in a film rendered at 24 Frames per second, there would be 24 frames of animation for each character and such. Animating in twos is when something is animated so that an image is displayed for two frames as opposed to only one. This effect can be taken a step further by animating in threes, fours and so on. With this method, the animation has a more choppy look. Additionally, characters hold a pose for longer bringing more emphasis to these poses. <br>
<img width="975" height="325" alt="image" src="https://github.com/user-attachments/assets/fd118216-33a0-4308-904f-0e4eb06001f9" />
I am currently working on a music video project with motion capture animation. The main problem was be to figure out how to turn my motion capture animations from 120 FPS and animated in ones to 24 FPS and animated in twos.<br>
<h2>The Tool</h2>
<h2>Setup</h2>
Before anything can happen, first we must understand how we can edit animations inside of Unreal Engine. Animations in Unreal are brought in as Animation Sequence assets. You can’t directly edit these animations in the Animation Sequence asset, you can only add additive layer tracks. In order to setup an environment in which you can edit an animation you have to bake it into an FK Control Rig and modify it in a Level Sequence asset. Thankfully, Unreal has a button to do this easily.<br>
<img width="534" height="341" alt="image" src="https://github.com/user-attachments/assets/08b95a35-0e33-4e09-be15-a18762821a58" />
<img width="379" height="343" alt="image" src="https://github.com/user-attachments/assets/3f91773d-cc44-4cf2-9fd0-41aa7d9d4ec7" />
<img width="963" height="452" alt="image" src="https://github.com/user-attachments/assets/01eb34f7-a178-406b-97f2-af58e944af3f" />
As mentioned earlier, the motion capture footage we got was recorded in 120 FPS. The first step is to change the frame rate for that footage to 24 FPS to match the frame rate of the film. This can be done by editing the animation in Unreal using a Level Sequencer or by bringing it by a DCC of your choice such as Autodesk Maya. Now with an environment to edit animations within Unreal, we must be able to turn animation into twos, threes, or fours. The theory is that we would hold a keyframe for two, three, or four frames at a time. In practice, we have to copy a keyframe over to the next couple for frames. To understand the amount of data that needs to be moved, one must understand how the Level Sequencer in Unreal works.<br>
<img width="992" height="358" alt="image" src="https://github.com/user-attachments/assets/936311de-9488-442e-93d7-7de6ab9520aa" /><br>
_animation in ones_
<img width="975" height="361" alt="image" src="https://github.com/user-attachments/assets/6cb7c62e-3fe4-47fc-aff0-9d787ba763eb" /><br>
_animation in twos_
<h2>Level Sequencer</h2>
<img width="883" height="411" alt="image" src="https://github.com/user-attachments/assets/88520420-577e-4b6d-84e0-69529e60ed84" />
The sequencer consists of various levels. First a binding (Skeleton), this consists of tracks (FKControlRig). Then every track has sections (HeadEnd or any joint). Every section has channels (Location.X). Lastly, these channels contain keys (keyframes).<br>
So we need to be able to access all of these for a Level Sequence. This can be done with Python thanks to the Sequencer Scripting Plugin that comes with Unreal by default. <br>
<h2>Code:</h2>
There are three main functions and one helper function. The functions are written in Python and saved as a separate file. These functions are called by an Editor Utility Widget which also provides the basic UI.<br>
<img width="958" height="562" alt="image" src="https://github.com/user-attachments/assets/b97b5209-4b5e-43ed-bbd3-a417d2e19668" />
<img width="509" height="352" alt="image" src="https://github.com/user-attachments/assets/6bf2f535-ca84-4be7-801b-cdbd75942e6f" />
<h2>Functions</h2>
<h2>stylize_anim</h2>
stylize_anim uses various asset paths to Level Sequence assets and stylizes each one based on the parameter framesToSkip. First we initialize a transaction to make our changes reversible. Then we loop through every channel in every joint. Once we have a channel, we run our helper function stylize_channel<br>
<img width="975" height="561" alt="image" src="https://github.com/user-attachments/assets/604e84d3-6f36-491d-89d4-2b06c0c241ac" />
<h2>stylize_channel</h2>
This function grabs a channel and loops through all of the keys. This is where the logic for keeping and copying the frames happens. First, we check the frame number and apply a modulo operation with the number of frames to skip. We do a modulo because it gives us valuable results that tell us what to do with the current keyframe. <br>
When the result is 0, this means the current frame number is a multiple of frames_to_skip. This is important because this means that we want to keep this keyframe, so we save the value in key_value.<br>
If the result is one less than frames_to_skip, this means that the next frame we will be saving the keyframe, so we want to paste key_value into this frame.<br>
If the result is anything else, we delete the keyframe.<br> 
So now, we have a range of frames where we are holding the pose and all the frames in between are deleted. No more interpolation. Filtering out the frames also gives us that advantage of doing key reduction and optimizing our animation file. This is an example scenario:<br>
If we are changing our animation to 3s, the key at frame 0 would be saved ( 0 % 3 = 0), frame 1 would be deleted ( 1 % 3 = 1), and frame 2 would copy frame 0’s value ( 2 % 3 = 2; 2 == (3 – 1)).<br>
<img width="928" height="489" alt="image" src="https://github.com/user-attachments/assets/0fa4587c-36cd-4e3d-abde-03f75db3cd11" />
<h2>stylize_channel</h2>
This function loops through all the selected channels and runs stylize_channel. In order to facilitate, we use the function get_selected_channels. This returns an array of channels as Channel Proxy type objects. With this data type we can’t do much. We must convert them into Movie Scene Scripting Channel type objects. To do this, we go up a level and go to the section, then from there we look for the channels and find the ones the user had selected by comparing the names.<br>
<img width="975" height="200" alt="image" src="https://github.com/user-attachments/assets/36365a7e-fe65-45af-862b-e137b1478491" />
<h2>bake_selected_channels</h2>
This function is used to bake channels. I added this function because I decided I wanted to make my background assets to match the style of my dance sequences. Mostly the fire movement and also the windmill rotation. In order to apply the stylization, first we have to have enough keyframes. This is the main utility of this function. It selects a channel and calculates its rate of change (or slope, change in value/change in frame number). Then it creates all the keyframes in between. This assumes linear change. <br>
<img width="975" height="263" alt="image" src="https://github.com/user-attachments/assets/aa60b460-19a1-4b21-952f-6233478a671a" />
<h2>Reflection</h2>
I really enjoyed working on this project. I have some experience writing tools for Maya when I want to save myself some clicks. Usually, those are very specific to my work and I don’t add a lot of reusability. For this tool I wanted to make sure that it was generally useful for a wider amount of people not just myself. I encountered a lot of issues earlier on because I couldn't find proper documentation or code examples. After finding some examples everything became much simpler. I read though the code to understand the functions that are being used. I learned a lot about the Unreal Engine Sequencer and it has a lot of potential in CG pipelines. I will try to write more tools on my own time.
