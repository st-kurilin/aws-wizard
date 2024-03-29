import Link from "next/link";
import Layout from "./Layout";
import Section from "../components/Section";
import Ul from "../components/Ul";

export default props => (
    <Layout>
        <div>
            <br/>
            <br/>
            <img src="/static/aws_logo.svg" style={{width: "100%", maxHeight: 200}}/>
            <br/>
            <br/>
        </div>
        <div>
            <Section>
                <h5>AWS Account Configuration</h5>
                Before you start using AWS-Wizard you need to have Amazon account created and CLI installed.
                Since you are using our deploy script this is where most manual work from you required.
                However, don't worry we've written that tutorial to get you on quick.
            </Section>
            <Section>
                <Ul>{[<div key="signup">
                    <h6>AWS Sign Up</h6>
                    <p>
                        Create an account via <a href="https://portal.aws.amazon.com/billing/signup" target="_blank">aws
                        site.</a>
                        It's required to specify a credit card and phone number.
                        However, you are likely to pay nothing for the first year.
                    </p>
                </div>,
                    <div key="user">
                        <h6>Create User for Remote Control</h6>
                        <p>
                            Create a new user on <a href="https://console.aws.amazon.com/iam/" target="_blank">IAM
                            service</a>.
                        </p>
                        <ul>
                            <li>"Programmatic access" should be marked</li>
                            <li>Use existing role "AdministratorAccess" to provide user permissions</li>
                            <li>You will need "AWS Access Key ID" and "AWS Secret Access Key" in further steps</li>
                        </ul>

                    </div>,
                    <div key="dcli">
                        <h6>Download AWS CLI</h6>
                        The latest version is available at <a href="https://console.aws.amazon.com/iam/"
                                                              target="_blank">CLI website</a>.
                    </div>,
                    <div key="ccli">
                        <h6>Configure AWS CLI</h6>
                        Once AWS CLI downloaded you can run "aws configure". Default options are fine.
                        You've already obtained "AWS Access Key ID" and "AWS Secret Access Key" for remote control user.
                    </div>
                ]}</Ul>
            </Section>
        </div>
    </Layout>
);

export const AwsAccountLink = props => (
    <Link href='/aws-account'>
        <a href="/aws-account"
           className={props.className}>
            Configure AWS Account
        </a>
    </Link>
);
