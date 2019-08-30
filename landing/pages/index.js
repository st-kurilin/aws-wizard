import Link from "next/link";
import Nav from "../components/Nav";
import Hero from "../components/Hero";
import Feature from "../components/Feature";
import Section from "../components/Section";
import Footer from "../components/Footer";
import ParallaxImg from "../components/ParallaxImg";

const Index = () => (
    <div>
        <Nav />
        <Hero header="AWS Wizard" subheader="Amazon made simple.">
            <StaticWebsiteLink />
        </Hero>
        <div>
            <Section>
                <Feature title="Speed Ups" icon="flight_takeoff">
                    You can get started with AWS easily, and focus on solving important problems instead of dealing with
                    deployment.
                </Feature>
                <Feature title="Best Practices" icon="flash_on">
                    You don't need to know infrastructure patterns to follow them.
                    Simple deploy script will provide abstraction that you need to allow you follow best practices
                    effortlessly.
                </Feature>
                <Feature title="Free to Go" icon="lock_open">
                    We provide a script for deployments. No need to include any runtime dependencies.
                    Stay with us only if you 100% satisfied. Not because of vendor lock in.
                </Feature>
            </Section>
            <ParallaxImg
                text="No need to hire devops any more. If you already have one, let him enjoy vacation.">
                background2.jpg
            </ParallaxImg>
            <Section>
                <div className="col s12 center">
                    <h3><i className="mdi-content-send brown-text"></i></h3>
                    <h4>Deploy Easily</h4>
                    <p className="left-align light">
                        AWS is focused on enterprise clients that can afford to have a dedicated dev-ops engineers.
                        AWS-Wizard makes it easy to use all infrastructure from AWS without special skills.
                        It automates all the error-prone deployment and configuration tasks, and sets everything up the way developers expect out of the box.
                        <br/>
                        This means that you can get started with AWS microservices easily, and focus on solving important business problems instead of dealing with AWS deployment workflows.
                        <br/>
                        Cloudfront/Terraform/Ansible helps devops to build complex solutions.
                        AWS-Wizard allows you to go without devops using simple solutions.
                    </p>
                </div>
            </Section>
            <ParallaxImg
                text="You don't need to invent wheel for each new project. Someone already solved that infrastructure issue.">
                background3.jpg
            </ParallaxImg>
            <Section>
                <Feature title="Static Website" icon="web">
                    Amazon provides powerful technologies to support static websites.
                    Unlimited scaling with S3. HTTPS support with free Amazon Certificate. Global distribution with
                    CloudFront.
                    Configuring all this technologies used to be a hustle. Not anymore.
                    Recommended approach if you don't need any backend.
                    <StaticWebsiteLink/>
                </Feature>
                <Feature title="Lambda Backend" icon="build">
                    Continuous scaling with cutting edge backend solution from Amazon.
                    It the optimal solution in terms of cost and time effort.
                    All major languages are supported including Python, Node.js, Java and Go.
                    However there are some limitations with frameworks usage.
                    Recommended approach for new projects that needs backend.
                    <ServerlessLink/>
                </Feature>
                <Feature title="EC2 Backend" icon="developer_board">
                    EC2 is bread and butter for Amazon. The ultimate solution with virtual machines.
                    Now you can run your solution in auto-scalable infrastructure with a single command.
                    No limitation on technology used. All programming languages and frameworks supported.
                    Recommended approach if you are migrating existing solution to cloud.
                    <ServerLink/>
                </Feature>
            </Section>
            <ParallaxImg
                text="Spend time on what brings value. Trust us to help you with infrastructure that will support you.">background2.jpg</ParallaxImg>
        </div>
        <Footer/>
    </div>
);

const StaticWebsiteLink = props => <div className="row center">
    <br/>
    <Link href='/static-website'>
        <a href="/static-website"
           className="btn-large waves-effect waves-light teal lighten-1">
            Build Static Website
        </a>
    </Link>
    <br/>
</div>;

const ServerlessLink = props => (
    <div className="row center">
        <br/>
        <span
           className="btn-large waves-effect waves-light grey lighten-1">
            Coming Soon..
        </span>
        <br/>
    </div>
);

const ServerLink = ServerlessLink;
export default Index;