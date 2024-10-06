import './App.css';
import './tw.css';
import './particle.scss';
import './tw.css';
import './particle.scss';
import VideoBar from './components/videoBar/VideoBar';
import Hls from 'hls.js';
import React, { Component, useRef, useEffect } from 'react';

function App() {

  const videoRef = useRef(null);

  useEffect(() => {
    const hls = new Hls();
    const video = videoRef.current;
    const hlsUrl = 'https://1026fd8e9fc3.ngrok.app/stream.m3u8'; // URL to your HLS stream

    if (Hls.isSupported()) {
      hls.loadSource(hlsUrl);
      hls.attachMedia(video);
      hls.on(Hls.Events.MANIFEST_PARSED, function () {
        video.play();
      });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = hlsUrl;
      video.addEventListener('loadedmetadata', function () {
        video.play();
      });
    }

    return () => {
      hls.destroy();
    };
  }, []);

  return (
    <div className="App">
      <div id="particle-container">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>

      </div>
      <div className='h-[12vh] mt-4 mb-6'>
        <nav className='flex place-content-center h-full w-[60vw] mx-auto'>
          <a className='h-full w-1/5'><img src="./assets/cct-logo-white.png" className="w-full" /></a>
          <a href="#vid1" className='hover:bg-white w-1/8 flex hover:text-purple-900 font-bold h-4/6 m-auto ml-1'><p className='m-auto'>Recent</p></a>
          <a href="#vid2" className='hover:bg-white flex hover:text-purple-900 font-bold h-4/6 m-auto'><p className='m-auto'>Favorites</p></a>
          <a href="#" className='hover:bg-white flex hover:text-purple-900 font-bold h-4/6 m-auto'><p className='m-auto'>Somethin'</p></a>
          <a href="#" className='hover:bg-white flex hover:text-purple-900 font-bold h-4/6 m-auto'><p className='m-auto'>Somethin'</p></a>
        </nav>
      </div>

      <section className="h-[82vh] px-[14%] text-left box-border display-block mb-12">
        <h1 className="h-[10%] text-5xl">Latest Clip/Feed</h1>
        <video
          className="w-full h-[90%]"
          ref={videoRef}
          controls
          autoPlay
          muted
        ></video>
      </section>


      <VideoBar id="vid1" entitle="Recently Saved" thumbs={10} />
      <VideoBar id="vid2" entitle="Favorite Clips" thumbs={10} />

      {/* <section id="blackout" className="w-screen h-screen absolute opacity-70 bg-black">
        asdf
      </section> */}

    </div>
  );
}

export default App;
