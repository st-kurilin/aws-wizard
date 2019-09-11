import Link from "next/link";
import Section from "../components/Section";
import Ul from "../components/Ul";
import {AwsAccountLink} from "./aws-account";
import Layout from "./Layout";


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
                <h5>Elastic Cloud Computing</h5>
                Amazon provides virtual computers to rent.
                You can run your computer applications on them just like with normal computers.
                The number of computers will be scaled according to your needs and budget.
            </Section>
            <Section>
                <h5>End Result</h5>
                <Ul>{[
                    <span key="index"><b>EC2</b> instances running from pre-configured image</span>,
                    <span key="https"><b>Autoscaling</b> according to configured rules</span>,
                    <span key="https"><b>Load balancer</b> to handle requests from users</span>,
                ]}
                </Ul>
            </Section>
            <Section>
                <h5>Prerequisites</h5>
                <Ul>{[
                    <div key="aws">
                        <span><b>AWS account</b> created and CLI configured.</span>
                        <p>
                            We have a tutorial on how to do it: <AwsAccountLink/>.
                        </p>
                    </div>,
                    <div key="aws">
                        <span><b>AWS wizard</b> installed.</span>
                        <p>
                            If not, just run `pip install awswizard`
                        </p>
                    </div>,
                ]}</Ul>
            </Section>
            <Section>
                <h5>Do it</h5>
                <Ul>{[
                    <span key="run-proto">
                         <p><b>Run Server</b> with <Wcmd>run-server boom</Wcmd></p>
                     </span>,
                    <span key="conf">
                         <p><b>Configure</b> Upload your application to server and make it run on start.
                             To connect to server you can use <Wcmd>connect-to-server boom</Wcmd></p>
                     </span>,
                    <span key="img">
                         <p><b>Create image</b> from this server by executing <Wcmd>create-image boomer --image-name boomering</Wcmd>
                         </p>
                     </span>,
                    <span key="killproto">
                         <p><b>Kill server</b> since we don't need server anymore <Wcmd>kill-server boomer</Wcmd>
                         </p>
                     </span>,
                    <span key="run-group">
                         <p>
                             <b>Run Group</b> of servers with <Wcmd>run-server-group boomboom --image-name boomer --max-size 8</Wcmd>
                        </p>
                     </span>,
                    <span key="enjoy">
                        <b>Enjoy!</b>
                        <p>Really, it should be done once all changes are propagated within Amazon infrastructure.
                            If something went wrong it's safe to run the script again. It's safe to contact us too.</p>
                    </span>,
                    <span key="clenup">
                        <p><b>Clean up</b> resources to avoid unnecessary charges. <br/>
                            Delete servers group <Wcmd>kill-server-group boomboom</Wcmd>.<br/>
                            Deleting image <Wcmd>delete-image boomer</Wcmd>.
                        </p>
                     </span>
                ]}
                </Ul>
            </Section>
        </div>
    </Layout>
);

const Wcmd = props => <span>&nbsp;<code>python -m awswizard {props.children}</code>&nbsp;</span>;

export const Ec2BackendLink = props => (
    <Link href='/ec2-backend'>
        <a href="/ec2-backend"
           style={props.style}
           className={props.className}>
            Run on EC2
        </a>
    </Link>
);

