import React from 'react'
import App from 'next/app'


class MyApp extends App {
    componentDidMount() {
        init();
    }
    componentDidUpdate () {
        init();
    }
    render() {
        const { Component, pageProps } = this.props;
        return <Component {...pageProps} />
    }
}

const init = () => {
    try {
        $('.sidenav').sidenav();
        $('.parallax').parallax();
    } catch (e) {
        //JQuery is not loaded yet or elements not ready
        setTimeout(init, 1000);
    }
};

export default MyApp