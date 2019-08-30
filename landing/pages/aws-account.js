import Link from "next/link";
import Nav from "../components/Nav";
import Section from "../components/Section";
import Footer from "../components/Footer";

export default props => (
    <div>
        <Nav />
        <div>
            <br/>
            <br/>
            <img src="/static/aws_logo.svg" style={{width: "100%", maxHeight: 200}}/>
            <br/>
            <br/>
        </div>
        <div>
            <Section>
                Before you start using AWS-Wizard you need to have Amazon account created and CLI installed.
                Since you are using our deploy script this is where most manual work from you required.
                However, don't worry we've write that tutorial to get you on quick.
            </Section>
            <Section>
                <ul className="collection">
                    <li className="collection-item">
                        <h6>AWS Sign Up</h6>
                        <p>
                            Create account via <a href="https://portal.aws.amazon.com/billing/signup" target="_blank">aws
                            site</a>.
                            It's required to specify credit card and phone number. However, you are likely to pay
                            nothing for the first year.
                        </p>
                    </li>
                    <li className="collection-item">
                        <h6>Create User for Remote Control</h6>
                        <p>
                            Create a new user on <a href="https://console.aws.amazon.com/iam/" target="_blank">IAM
                            service</a>.
                            <ul>
                                <li>"Programmatic access" should be marked</li>
                                <li>Use existing role "AdministratorAccess" to provide user permissions</li>
                                <li>You will need "AWS Access Key ID" and "AWS Secret Access Key" in futher steps</li>
                            </ul>
                        </p>
                    </li>
                    <li className="collection-item">
                        <h6>Download AWS CLI</h6>
                        The latest version is available at <a href="https://console.aws.amazon.com/iam/"
                                                              target="_blank">CLI website</a>.
                    </li>
                    <li className="collection-item">
                        <h6>Configure AWS CLI</h6>
                        Once AWS CLI downloaded you can run "aws configure". Default options are fine.
                        You've already obtained "AWS Access Key ID" and "AWS Secret Access Key" for remote control user.
                    </li>
                </ul>
            </Section>
        </div>
        <Footer/>
    </div>
);

export const AwsAccountLink = props => (
    <Link href='/aws-account'>
        <a href="/aws-account"
           className={props.className || "btn-large waves-effect waves-light teal lighten-1"}>
            Configure AWS Account
        </a>
    </Link>
);
