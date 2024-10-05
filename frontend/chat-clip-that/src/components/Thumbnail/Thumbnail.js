import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Display } from 'phaser';

const style = {
   width: '20vw',
   height: '85%',
   backgroundColor: 'blue',
   // margin: '1% 2% ',
   // display: 'inline-block',
   // whiteSpace: 'normal',
   // overflow: 'hidden',
};

const Thumbnail = () => (
   <iframe src="https://i.pinimg.com/originals/14/84/ae/1484ae77d2f40286b01089c31339b7b2.jpg" class="w-1/5 bg-blue-500 h-4/6 mx-9 inline-block whitespace-normal align-middle flex-shrink-0">
      VideoBar Component
   </iframe>
);

export default Thumbnail;
