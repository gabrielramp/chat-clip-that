import React from 'react';
import Thumbnail from '../Thumbnail/Thumbnail';
import '../../App.css';
import '../component.css';
import PropTypes from 'prop-types';

const VideoBar = (props) => (
   <section className="w-ful h-[30vh] place-content-around place-items-center mb-96 flex">
      <button onClick={() => sideScrollVidBar(props.id, true)} class="h-1/4 ml-12 w-[3.5%] rounded-full align-middle">&lt;</button>
      <div id={props.id} class="overflow-x-scroll w-10/12 h-full overflow-y-hidden whitespace-nowrap mx-auto flex place-items-center">
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
         <Thumbnail />
      </div>
      <button onClick={() => sideScrollVidBar(props.id, false)} class="h-1/4 mr-12 w-[3.5%] rounded-full align-middle">&gt;</button>

   </section>

);

const sideScrollVidBar = function (id, left) {
   let vidbar = document.getElementById(id);
   let scrollOffset = vidbar.children[1].offsetLeft - vidbar.firstChild.offsetLeft;
   let horizonty = left ? vidbar.scrollLeft - scrollOffset : vidbar.scrollLeft + scrollOffset;
   vidbar.scroll({
      top: 0,
      left: horizonty,
      behavior: "smooth",
   });
   console.log(left ? "Left" : "right");
   console.log(vidbar.firstChild.scrollWidth);
};

VideoBar.propTypes = {};

VideoBar.defaultProps = {};

export default VideoBar;
