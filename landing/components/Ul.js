export default props => (
    <ul className="collection">
        {props.children.map((l, i) => <li className="collection-item" key={i}>{l}</li>)}
    </ul>
);