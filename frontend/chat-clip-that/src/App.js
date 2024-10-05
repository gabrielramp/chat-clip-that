import './App.css';
import './tw.css';
import React, { Component } from 'react';
import VideoBar from './components/videoBar/VideoBar';

function App() {
  return (
    <div className="App">
      <div>
        <nav>
          <a href="#"><p>Somethin'</p></a>
          <a href="#"><p>Somethin'</p></a>
          <a href="#"><p>Somethin'</p></a>
          <a href="#"><p>Somethin'</p></a>
        </nav>
      </div>

      <section class="h-[85vh] px-[13%] text-left box-border display-block mb-12">
        <h1 class="h-[10%] text-5xl">Latest Clip/Feed</h1>
        <iframe class="w-full h-[90%]" src="https://en.wikipedia.org/wiki/Wikipedia:Dark_mode"></iframe>
      </section>
      
        <VideoBar id="vid1"/>
       
      asdf
    </div>
  );
}

export default App;
