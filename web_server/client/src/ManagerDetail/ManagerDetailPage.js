import React from 'react';
import PropTypes from 'prop-types';
import io from 'socket.io-client';
let socket = io(`http://localhost:4000/console/client`);


class ManagerDetailPage extends React.Component {

    constructor(props, context) {
        super(props, context);
        // set the initial component state
        this.state = {
            pid: this.props.params.pid,
            name: null,
            children: []
        };

        socket.on('connect', function () {
            console.log("web socket connected on manager detail");
            socket.emit('get-managers', {});
        });

        socket.on('disconnect', function () {
            console.log("web socket disconnected on manager detail");
        });
    }
    componentDidMount() {
        // socket.
    }

    render() {
        return (
            <div className="row">
                <p>PID: {this.state.pid}</p>
                <p>Name: {this.state.name}</p>
                <p>Healthy: {this.state.healthy}</p>
                <p>Last Beat: {this.state.lastBeat}</p>
            </div>
        );
    }
}

// To make react-router work
ManagerDetailPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default ManagerDetailPage;
