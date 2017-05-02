import './NewsPanel.css';
import React from 'react';
import NewsCard from '../NewsCard/NewsCard'

export default class NewPanel extends React.Component {

    constructor() {
        super();
        this.state = { "news": null };
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
        const port = "4000";
        const host = "localhost"
        const endpoint = `http://${host}:${port}/news`;
        let request = new Request(endpoint, {
            method: 'GET',
            cache: false
        });

        fetch(request)
            .then(res => res.json())
            .then((news) => {
                console.log("get news: " + news);
                this.setState({
                    "news": this.state.news ? this.state.news.concat(news) : news
                })
            }).catch(err => console.error(err))
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