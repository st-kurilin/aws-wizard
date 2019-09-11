import Link from "next/link";
import {StaticWebsiteLink} from "../pages/static-website";
import {AwsAccountLink} from "../pages/aws-account";
import {Ec2BackendLink} from "../pages/ec2-backend";


export default () => <nav className="white" role="navigation">
    <div className="nav-wrapper container">
        <Link href='/'>
            <a id="logo-container" href="/" className="brand-logo">AWS Wizard</a>
        </Link>


        <ul className="right hide-on-med-and-down">
            <li><StaticWebsiteLink/></li>
            <li><Ec2BackendLink/></li>
        </ul>

        <ul id="nav-mobile" className="sidenav">
            <li onClick={removeOverlay}><AwsAccountLink /></li>
            <li>&nbsp;</li>
            <li onClick={removeOverlay}><StaticWebsiteLink /></li>
            <li onClick={removeOverlay}><Ec2BackendLink /></li>
            <li>&nbsp;</li>
            <li><a  href="https://github.com/st-kurilin/aws-wizard" target="_blank">Github</a></li>
        </ul>
        <a href="#" data-target="nav-mobile" className="sidenav-trigger"><i className="material-icons">menu</i></a>
    </div>
</nav>
const removeOverlay = () => {
    //remove overlay when side nav used
    setTimeout(() => {
        for (let item of document.getElementsByClassName("sidenav-overlay")) {
            item.remove();
        }
    }, 500);
};