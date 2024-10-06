import React, { useState, useEffect } from 'react';
import Thumbnail from '../Thumbnail/Thumbnail';
import '../../App.css';
import '../component.css';
import PropTypes from 'prop-types';

const VideoBar = (props) => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    // Fetch the list of videos from the server
    fetch('https://knighthacks2024.ngrok.app/api/videos')
      .then((response) => response.json())
      .then((data) => {
        // Sort videos by date extracted from filenames
        const sortedVideos = data.sort((a, b) => parseDate(b) - parseDate(a));
        setVideos(sortedVideos);
      })
      .catch((error) => {
        console.error('Error fetching videos:', error);
      });
  }, []);

  const desiredThumbnailCount = 5; // Set the desired number of thumbnails

  // Build the list of thumbnails, using placeholders if necessary
  const totalThumbnails = [];

  for (let i = 0; i < desiredThumbnailCount; i++) {
    if (i < videos.length) {
      totalThumbnails.push(
        <Thumbnail
          id={`${props.id}thumb${i}`}
          key={`${props.id}${i}`}
          video={videos[i]}
        />
      );
    } else {
      // Placeholder thumbnail
      totalThumbnails.push(
        <div
          key={`placeholder-${i}`}
          className="w-40 h-40 bg-purple-500 inline-block m-2"
        ></div>
      );
    }
  }

  return (
    <section>
      <h2 className="text-left text-3xl pl-44">{props.entitle}</h2>
      <div className="w-full h-[27vh] place-content-around place-items-center mb-10 flex">
        <button
          onClick={() => sideScrollVidBar(props.id, true)}
          className="h-1/4 ml-12 w-[3.5%] rounded-full align-middle font-black"
        >
          &lt;
        </button>
        <div
          id={props.id}
          className="overflow-x-scroll w-10/12 h-full overflow-y-hidden whitespace-nowrap mx-auto flex place-items-center"
        >
          {totalThumbnails}
        </div>
        <button
          onClick={() => sideScrollVidBar(props.id, false)}
          className="h-1/4 mr-12 w-[3.5%] rounded-full align-middle"
        >
          &gt;
        </button>
      </div>
    </section>
  );
};

const parseDate = (filename) => {
  // Assume filename is in 'MM-DD-HMM[AM/PM].mp4' format
  const nameWithoutExt = filename.replace('.mp4', '');
  const parts = nameWithoutExt.split('-');
  if (parts.length !== 3) return 0;

  const [month, day, timeWithPeriod] = parts;
  const timeMatch = timeWithPeriod.match(/(\d+)(AM|PM)/);
  if (!timeMatch) return 0;

  let hour = parseInt(timeMatch[1], 10);
  const period = timeMatch[2];

  if (period === 'PM' && hour !== 12) hour += 12;
  if (period === 'AM' && hour === 12) hour = 0;

  const date = new Date();
  date.setMonth(parseInt(month, 10) - 1);
  date.setDate(parseInt(day, 10));
  date.setHours(hour);
  date.setMinutes(0);
  date.setSeconds(0);

  return date.getTime();
};

const sideScrollVidBar = function (id, left) {
  let vidbar = document.getElementById(id);
  let scrollOffset = vidbar.children[1].offsetLeft - vidbar.firstChild.offsetLeft;
  let horizonty = left ? vidbar.scrollLeft - scrollOffset : vidbar.scrollLeft + scrollOffset;
  vidbar.scroll({
    top: 0,
    left: horizonty,
    behavior: 'smooth',
  });
};

VideoBar.propTypes = {
  entitle: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
};

VideoBar.defaultProps = {};

export default VideoBar;
