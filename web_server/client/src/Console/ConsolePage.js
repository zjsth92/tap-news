import React from 'react';
import PropTypes from 'prop-types';
import ConsoleCard from './ConsoleCard'
import io from 'socket.io-client';
let socket = io(`http://localhost:4000/console/client`);


class ConsolePage extends React.Component {

    constructor(props, context) {
        super(props, context);

        // set the initial component state
        this.state = {
            managers: []
        };

        socket.on('connect', function () {
            console.log("web socket connected");
        });

        socket.on('disconnect', function () {
            console.log("web socket disconnected");
        });

    }
    componentDidMount() {
        console.log('console page did mount');
        socket.on('managers', (managers) => {
            console.log(managers);
            this.setState({
                managers: managers
            });
        });
        socket.emit('get-managers', {});
    }

    componentWillUnmount() {
        console.log('console page will unmount');
    }

    goToManagerDetail(pid) {
        this.context.router.push(`/console/managers/${pid}`);
    }

    renderAllManagers() {
        let services_list = this.state.managers.map((manager) => {
            return (
                <div className="col s4" key={manager.pid}>
                    <ConsoleCard manager={manager} showDetail={() => { this.goToManagerDetail(manager.pid) }} />
                </div>
            );
        });
        return (
            <div className="container">
                <div className='row'>
                    {services_list}
                </div>
            </div>
        );
    }

    render() {
        return (
            <div>
                {this.renderAllManagers()}
            </div>
        );
    }
}

// To make react-router work
ConsolePage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default ConsolePage;
