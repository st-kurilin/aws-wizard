import Head from 'next/head'
import Nav from "../components/Nav";
import Footer from "../components/Footer";

export default ({ children, title = 'AWS Wizard' }) => (
    <div>
        <Head>
            <title>{title}</title>
            <meta charSet='utf-8' />
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"/>
            <link rel="stylesheet"
                  href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"/>
            <link href="static/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
        </Head>
        <Nav />
        {children}
        <Footer/>
    </div>
)