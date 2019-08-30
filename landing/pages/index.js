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
        <Hero header="AWS Wizard" subheader="AWS made simple">
            <Link href='/static-website'>
                <a href="/static-website"
                   className="btn-large waves-effect waves-light teal lighten-1">
                    Get Started
                </a>
            </Link>
        </Hero>
        <div>
            <Section>
                <Feature  title="Speed Ups" icon="flash_on">A modern responsive front-end framework based on Material
                    Design</Feature>
                <Feature title="Speed Ups" icon="flash_on">A modern responsive front-end framework based on Material
                    Design</Feature>
                <Feature title="Speed Ups" icon="flash_on">A modern responsive front-end framework based on Material
                    Design</Feature>
            </Section>
            <ParallaxImg
                text="A modern responsive front-end framework based on Material Design">background2.jpg</ParallaxImg>
            <Section>
                <div className="col s12 center">
                    <h3><i className="mdi-content-send brown-text"></i></h3>
                    <h4>Contact Us</h4>
                    <p className="left-align light">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
                        scelerisque id nunc nec volutpat. Etiam pellentesque tristique arcu, non consequat magna
                        fermentum ac. Cras ut ultricies eros. Maecenas eros justo, ullamcorper a sapien id, viverra
                        ultrices eros. Morbi sem neque, posuere et pretium eget, bibendum sollicitudin lacus. Aliquam
                        eleifend sollicitudin diam, eu mattis nisl maximus sed. Nulla imperdiet semper molestie. Morbi
                        massa odio, condimentum sed ipsum ac, gravida ultrices erat. Nullam eget dignissim mauris, non
                        tristique erat. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia
                        Curae;</p>
                </div>
                <ParallaxImg
                    text="A modern responsive front-end framework based on Material Design">background3.jpg</ParallaxImg>
            </Section>
        </div>
        <Footer/>
    </div>
);

export default Index;