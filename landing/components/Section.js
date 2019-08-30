export default props => {
    return <div className="container">
        <div className="section">
            <div className="row">
                {props.children}
            </div>
        </div>
    </div>
};