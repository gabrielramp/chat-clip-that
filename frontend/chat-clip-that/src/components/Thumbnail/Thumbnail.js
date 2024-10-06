import React from 'react';
import PropTypes from 'prop-types';

const Thumbnail = ({ id, video }) => (
  <div id={id} className="thumbnail">
    <a href={`https://knighthacks2024.ngrok.app/finished-edited-clips/${video}`} download>
      <video
        width="160"
        height="90"
        controls={false}
        preload="metadata"
        className="video-thumbnail"
      >
        <source src={`https://knighthacks2024.ngrok.app/finished-edited-clips/${video}#t=0.5`} type="video/mp4" />
      </video>
    </a>
  </div>
);

Thumbnail.propTypes = {
  id: PropTypes.string.isRequired,
  video: PropTypes.string.isRequired,
};

export default Thumbnail;
