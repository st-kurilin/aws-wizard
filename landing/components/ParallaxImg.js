
export default props => <div className="parallax-container valign-wrapper">
    <div className="section no-pad-bot">
        <div className="container">
            <div className="row center">
                <h5 className="header col s12 light">{props.text}</h5>
            </div>
        </div>
    </div>
    <div className="parallax"><img src={"static/" + props.children} alt={props.children}/></div>
</div>