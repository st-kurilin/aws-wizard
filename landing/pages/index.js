import Link from "next/link";
import Nav from "../components/Nav";
import Hero from "../components/Hero";
import Content from "../components/Content";
import Footer from "../components/Footer";

const Index = () => (
    <div>
        <Nav/>
        <Hero/>
        <Content/>
        <Footer/>

        <Link href='/static-website'><p>GO STATIC</p></Link>
    </div>
);

export default Index;