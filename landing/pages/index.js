import Link from 'next/link';

const Index = () => (
    <div>
        <p>AWS wizard landing</p>
        <p>It's so cool.</p>
        <Link href='/static-website'><p>GO STATIC</p></Link>
    </div>
);

export default Index;