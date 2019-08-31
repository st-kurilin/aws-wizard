import {AwsAccountLink} from "../pages/aws-account";
import {StaticWebsiteLink} from "../pages/static-website";

export default props => <footer className="page-footer teal">
    <div className="container">
        <div className="row">
            <div className="col l6 s12">
                <h5 className="white-text">About Us</h5>
                <p className="grey-text text-lighten-4">
                    We are a team of developers who've got frustrated about how much time we need to spend on infrastructure for our own projects.
                    It's just not fun to do similar error prone configuration over and over again.
                    AWS-Wizard is our solution that allows to get infrastructure in place fast and with minimal manual work.
                </p>
            </div>
            <div className="col l3 s12">
                <h5 className="white-text">Quick Links</h5>
                <ul>
                    <li><AwsAccountLink className="white-text"/></li>
                    <li><StaticWebsiteLink className="white-text"/></li>
                </ul>
            </div>
            <div className="col l3 s12">
                <h5 className="white-text">Connect</h5>
                <ul>
                    <li><a className="white-text" href="mailto:st.kurilin@gmail.com?Subject=awswizzard" target="_top">st.kurilin@gmail.com</a></li>
                    <li><a className="white-text" href="https://www.linkedin.com/in/stan-kurilin/">Connect on LinkedIN</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div className="footer-copyright">
        <div className="container">
            Supported by <a className="brown-text text-lighten-3" href="https://gotostan.com">gotostan</a>
        </div>
    </div>
</footer>
