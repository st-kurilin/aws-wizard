import Document, {Html, Head, Main, NextScript} from "next/document";

class MyDocument extends Document {

    render() {
        console.log("MyDocument render");
        return (
            <Html>
            <Head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>


                <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"/>
                <link rel="stylesheet"
                      href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"/>
                <link href="static/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
            </Head>

            <body>
            <Main />
            <NextScript />
            <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            </body>
            </Html>
        )
    }
}

export default MyDocument