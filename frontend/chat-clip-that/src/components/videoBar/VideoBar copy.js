import React from 'react';
import Thumbnail from './Thumbnail';
import '../../App.css';
import PropTypes from 'prop-types';

const OutieStyle = {
   height: '30vh',
   width: '100%'
}

const InnieStyle = {
   height: '100%',
   width: '85%',
   backgroundColor: 'red',
   // display: 'inline',
   // textAlign: 'left',
   // margin: '0px',
   // marginLeft: 'auto',
   // marginRight: 'auto',
   // marginBottom: '100px',
   // // paddingLeft:'3vw',
   // // paddingRight:'3vw',
   // overflowX: 'scroll',
   // whiteSpace: 'nowrap',
   // // position:'relative',
   // overflowY: 'hidden',
   // scrollbarGutter: 'stable-both-edges'
}

const leftButtonStyle = {
   left: '2vw',
}

const rightButtonStyle = {
   right: '2vw'
}


const VideoBar = () => (
   <div style={OutieStyle}>
      <button class="horizontalButton" style={leftButtonStyle}>&lt;</button>

      <div class="overflow-x-scroll" style={InnieStyle}>
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
      <button class="horizontalButton" style={rightButtonStyle}>&rt;</button>
   </div>
);

VideoBar.propTypes = {};

VideoBar.defaultProps = {};

export default VideoBarC;
