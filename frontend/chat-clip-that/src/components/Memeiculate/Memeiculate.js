import React, { Component } from 'react';
let keyTrack = 700;

const Memeiculate = (props) => (
   <div id="memery-container" className="w-full h-full">
      {new Array(props.particles).fill("").map((index) => (
         <div key={keyTrack++} className="memery">
         </div>
      ))}
   </div>
);

export default Memeiculate;
