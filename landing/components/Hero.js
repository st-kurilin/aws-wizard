export default props => <div id="index-banner" className="parallax-container">
    <div className="section no-pad-bot">
        <div className="container">
            <br/><br/>
            <h1 className="header center teal-text text-lighten-4">{props.header}</h1>
            <div className="row center">
                <h5 className="header col s12 light">{props.subheader}</h5>
            </div>
            {props.children}
        </div>
    </div>
    <div className="parallax"><img src="static/background1.jpg" alt="Unsplashed background img 1"/></div>
</div>
