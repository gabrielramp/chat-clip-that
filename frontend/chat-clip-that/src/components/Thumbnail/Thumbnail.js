import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Display } from 'phaser';


const Thumbnail = (props) => (
   <iframe onClick ={() => miniPlayer(props.filepath)} src="" id={props.id} class="w-1/5 bg-blue-500 h-5/6 mx-9 inline-block whitespace-normal align-middle flex-shrink-0">
      VideoBar Component
   </iframe>
);

const miniPlayer = function (filepath) {
   // let grayer = document.getElementById();
   // let scrollOffset = vidbar.children[1].offsetLeft - vidbar.firstChild.offsetLeft;
   // let horizonty = left ? vidbar.scrollLeft - scrollOffset : vidbar.scrollLeft + scrollOffset;
   // vidbar.scroll({
   //    top: 0,
   //    left: horizonty,
   //    behavior: "smooth",
   // });
   // console.log(left ? "Left" : "right");
   // console.log(vidbar.firstChild.scrollWidth);
};

export default Thumbnail;
