export default props => <div className="col s12 m4">
    <div className="icon-block">
        <h2 className="center brown-text"><i className="material-icons">{props.icon}</i></h2>
        <h5 className="center">{props.title}</h5>

        <p className="light" style={{textAlign: "justify"}}>{props.children}</p>
    </div>
</div>;