import './NewsPanel.css';
import React from 'react';
import Auth from '../Auth/Auth';
import NewsCard from '../NewsCard/NewsCard'
import config from 'web_server_config'


export default class NewPanel extends React.Component {

    constructor() {
        super();
        this.state = {news:null, pageNum:1, totalPages:1, loadedAll:false};
    }

    componentDidMount() {
        this.loadMoreNews();
    }
    renderNews() {
        let news_list = this.state.news.map(function (news) {
            return (
                <a className='list-group-item' href="#">
                    <NewsCard news={news} />
                </a>
            );
        });

        return (
            <div className="container-fluid">
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        );
    }

    loadMoreNews() {
        const endpoint = `${config.load_more_news_endpoint}/userId/${Auth.getEmail()}/pageNum/${this.state.pageNum}`;
        let request = new Request(endpoint, {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            },
            cache: false
        });

        fetch(request)
            .then(res => res.json())
            .then((news) => {
                console.log(news);
                this.setState({
                    "news": this.state.news ? this.state.news.concat(news) : news
                })
            }).catch(err => console.error)
    }

    render() {
        if (this.state.news) {
            return (
                <div>
                    {this.renderNews()}
                </div>
            );
        } else {
            return (
                <div>
                    <div id='msg-app-loading'>Loading</div>
                </div>
            );
        }
    }

}