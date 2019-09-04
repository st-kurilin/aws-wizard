import {AwsAccountLink} from "../pages/aws-account";
import {StaticWebsiteLink} from "../pages/static-website";

export default props => <footer className="page-footer teal">
    <div className="container">
        <div className="row">
            <div className="col l6 s12">
                <h5 className="white-text">About Us</h5>
                <p className="grey-text text-lighten-4">
                    We are a team of developers who've got frustrated about how much time
                    we need to spend on infrastructure for our projects.
                    It's just not fun to do similar error-prone configuration over and over again.
                    AWS Wizard is our solution that allows getting the infrastructure
                    in place fast and with minimal manual work.
                </p>
            </div>
            <div className="col l3 s12">
                <h5 className="white-text">Quick Links</h5>
                <ul>
                    <li><AwsAccountLink className="white-text"/></li>
                    <li><StaticWebsiteLink className="white-text"/></li>
                    <li><a className="white-text" href="https://github.com/st-kurilin/aws-wizard" target="_blank">Source Code</a></li>
                </ul>
            </div>
            <div className="col l3 s12">
                <h5 className="white-text">Connect</h5>
                <ul>
                    <li><a className="white-text" href="mailto:st.kurilin@gmail.com?Subject=awswizzard" target="_top">st.kurilin@gmail.com</a></li>
                    <li><a className="white-text" href="https://www.linkedin.com/in/stan-kurilin/">Connect on LinkedIn</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div className="footer-copyright">
        <div className="container" style={{padding: 8}}>
            Supported by <a className="brown-text text-lighten-3" href="https://gotostan.com">gotostan</a>
        </div>
    </div>
</footer>
