import Link from "next/link";
import Nav from "../components/Nav";
import Feature from "../components/Feature";
import Section from "../components/Section";
import Footer from "../components/Footer";
import Ul from "../components/Ul";


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
                <h5>What is Static Website?</h5>
                It is a website which contains Web pages with fixed content. Just HTML, CSS, JavaScript and Images.
                No database or server-side rendering.
                This is ultimate solution for landing pages. Go one more step and get a blog with static site
                generators.
            </Section>
            <Section>
                <Feature title="Fast and Secure" icon="trending_up">
                    Your code will be distributed across the globe to serve the users from the nearest location.
                    It will be easy to cache it to speed up further. And since there are truly no server code all
                    security problems could be handled by Amazon.
                </Feature>
                <Feature title="Easy to Create" icon="event_seat">
                    You don't need to have any programming skills to create one.
                </Feature>
                <Feature title="Cheapest to Maintain" icon="monetization_on">
                    Having top-notch infrastructure could cost you $0.02 a day. It's not free, but it has unbeatable value.
                </Feature>
            </Section>
            <Section>
                <h5>Prerequisites</h5>
                <Ul>{["AWS account created and CLI configured.", "Domain purchased."]}</Ul>
            </Section>
            <Section>
                <h5>Do it</h5>
                <Ul>{[
                    <span><b>Install script</b> with `pip install aws-wizard`</span>,
                    <span>
                        <p><b>Run script</b> with `aws-wizard mydomain.com ./src`</p>
                        <p>The manual step is to link your domain to Amazon.
                            To do that you will need to provide NS records from script to your domain provider.
                            Just follow instructions from your providers. Here are the links for common ones:&nbsp;
                            <a href="https://www.godaddy.com/help/add-an-ns-record-19212"
                               target="_blank">GoDaddy,</a>&nbsp;
                            <a href="https://support.google.com/domains/answer/6353515"
                               target="_blank">Google Domains, </a>&nbsp;
                            <a href="https://www.namecheap.com/support/knowledgebase/article.aspx/434/2237"
                               target="_blank">namecheap.</a>
                        </p>
                    </span>,
                    <span>
                        <b>Enjoy!</b>
                        <p>Really, it should be done once all changes are propagated within Amazon infrastructure.
                            If something went wrong it's safe to run script again. It's safe to contact us too.</p>
                    </span>
                    ]}
                </Ul>
            </Section>
        </div>
        <Footer/>
    </div>
);


export const StaticWebsiteLink = props => (
    <Link href='/static-website'>
        <a href="/static-website"
           className={props.className}>
            Build Static Website
        </a>
    </Link>
);

