// import './NewsCard.css';
import React from 'react';
import PropTypes from 'prop-types';

const ConsoleCard = ({
  manager,
  showDetail
}) => (
<div className="card-panel">
    <p>Name: {manager.name}</p>
    <p>PID: {manager.pid}</p>
    <p>Host: {manager.host}</p>
    <p>Platform: {manager.platform}</p>
    <p>State: {manager.state}</p>
    <p>Total Memory: {manager.totalMemory.size}{manager.totalMemory.unit}</p>
    <button onClick={showDetail}>Show Detail</button>
</div>
);

ConsoleCard.propTypes = {
    manager: PropTypes.object.isRequired
};

export default ConsoleCard;