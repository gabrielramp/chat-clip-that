import React, { Component } from 'react';
let keyTrack = 900;

const Particulate = (props) => (
   <div id="particle-container" className="w-full h-full">
      {new Array(props.particles).fill("").map((index) => (
         <div key={keyTrack++} className="particle">
         </div>
      ))}
   </div>
);


export default Particulate;
// <div id={props.id} className="w-full h-full">
//    {new Array(props.particles).fill("").map((index) => (
//       <div key={keyTrack++} className="particle" />
//    ))}
// </div>