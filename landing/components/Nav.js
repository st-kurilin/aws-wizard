import Link from "next/link";
import {StaticWebsiteLink} from "../pages/static-website";
import {AwsAccountLink} from "../pages/aws-account";

export default () => <nav className="white" role="navigation">
    <div className="nav-wrapper container">
        <Link href='/'>
            <a id="logo-container" href="/" className="brand-logo">AWS-Wizard</a>
        </Link>


        <ul className="right hide-on-med-and-down">
            <li><AwsAccountLink/></li>
            <li><StaticWebsiteLink/></li>
        </ul>

        <ul id="nav-mobile" className="sidenav">
            <li><AwsAccountLink className=""/></li>
            <li><StaticWebsiteLink className=""/></li>
        </ul>
        <a href="#" data-target="nav-mobile" className="sidenav-trigger"><i className="material-icons">menu</i></a>
    </div>
</nav>