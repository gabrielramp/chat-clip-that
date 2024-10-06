import './Bones.css';
// import './Colors.css'
import './tw.css';
import './particle.scss';
import './App.css';

import VideoBar from './components/videoBar/VideoBar';
import Hls from 'hls.js';
import Particulate from './components/Particulate/Particulate';
import Memeiculate from './components/Memeiculate/Memeiculate';

import React, { Component, useRef, useEffect, useState } from 'react';

let theme = 0;

function App() {

  const videoRef = useRef(null);
  const [particles, setParticles] = useState(60);
  const [memery, setMemes] = useState(0);


  const changeMessage = (newPart) => {
    setParticles(newPart); // Update the prop
  };

  const toNormal = () => {
    if (theme == 0)
      return;
    theme = 0;
    let twitchSheet = document.getElementById('twitch-stylesheet');
    if (twitchSheet)
      document.head.removeChild(twitchSheet);
    let funnySheet = document.getElementById('funny-stylesheet');
    if (funnySheet)
      document.head.removeChild(funnySheet);
    document.getElementById('logo').src = './assets/cct-logo-white.png';
    setParticles(60);
    setMemes(0);
  }

  const toTwitch = () => {
    if (theme == 1)
      return;
    theme = 1;
    let styler = document.createElement('link');
    styler.rel = 'stylesheet';
    styler.href = 'Twitchy.css';
    styler.id = 'twitch-stylesheet'; // Add an id to easily find/remove it later
    document.head.appendChild(styler);
    let funnySheet = document.getElementById('funny-stylesheet');
    if (funnySheet)
      document.head.removeChild(funnySheet);
    document.getElementById('logo').src = './assets/cct-logo-twitch-filled.png'
    setParticles(0);
    setMemes(0);
  }

  const toFunny = () => {
    if (theme == 2)
      return;
    theme = 2;
    let styler = document.createElement('link');
    styler.rel = 'stylesheet';
    styler.href = 'Funny.css';
    styler.id = 'funny-stylesheet'; // Add an id to easily find/remove it later
    document.head.appendChild(styler);
    document.getElementById('logo').src = './assets/cct-logo-black.png';
    let twitchSheet = document.getElementById('twitch-stylesheet');
    if (twitchSheet)
      document.head.removeChild(twitchSheet);
    setParticles(0);
    setMemes(60);
  }

  useEffect(() => {
    const hls = new Hls();
    const video = videoRef.current;
    const hlsUrl = 'https://knighthacks2024.ngrok.app/hls_stream/stream.m3u8'; // URL to your HLS stream

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
      <Particulate particles={particles} />
      <Memeiculate particles={memery} />
      <div className='h-[12vh] mt-4 mb-6' id='nav-box'>
        <nav className='flex place-content-center h-full w-[60vw] mx-auto'>
          <a className='h-full w-1/5'><img id="logo" src="./assets/cct-logo-white.png" className="w-full" /></a>
          <a href="#vid1" className='navi w-1/8 flex font-bold h-4/6 m-auto ml-1'><p className='m-auto'>Clips</p></a>
          <a href="#" onClick={() => toNormal()} className='navi flex font-bold h-4/6 m-auto'><p className='m-auto'>Purple</p></a>
          <a href="#" onClick={() => toTwitch()} className='navi flex font-bold h-4/6 m-auto'><p className='m-auto'>Twitch-like</p></a>
          <a href="#" onClick={() => toFunny()} className='navi flex font-bold h-4/6 m-auto'><p className='m-auto'>Funny</p></a>
        </nav>
      </div>

      <section className="h-[82vh] px-[14%] text-left box-border display-block mb-12">
        <h1 className="h-[10%] text-5xl">Livestream</h1>
        <video
          className="w-full h-[90%]"
          ref={videoRef}
          controls
          autoPlay
          muted
        ></video>
      </section>


      <VideoBar id="vid1" entitle="Clips" thumbs={10} />

      <section id="blackout">
        Filler
      </section>

    </div>
  );
}



export default App;
