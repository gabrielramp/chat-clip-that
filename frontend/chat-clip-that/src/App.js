import './App.css';
import './tw.css';
import './particle.scss';

import React, { Component } from 'react';
import VideoBar from './components/videoBar/VideoBar';

function App() {
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

      <section class="h-[82vh] px-[14%] text-left box-border display-block mb-12">
        <h1 class="h-[10%] text-5xl">Latest Clip/Feed</h1>
        <iframe class="w-full h-[90%]" src="https://www.youtube.com/embed/CBEvfZu4HE4?si=ArnPmTBNB8xagJIL" title="YouTube video player" title="YouTube video player"></iframe>
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
