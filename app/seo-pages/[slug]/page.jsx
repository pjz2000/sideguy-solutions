import { notFound } from 'next/navigation';

import { getSeoPage, getAllSeoSlugs } from '@/lib/seoPages';



export function generateStaticParams() {

  return getAllSeoSlugs().map((slug) => ({ slug }));

}



export function generateMetadata({ params }) {

  const page = getSeoPage(params.slug);

  if (!page) return {};

  return {

    title: page.title,

    description: page.metaDescription,

    alternates: {

      canonical: `https://www.sideguysolutions.com/seo-pages/${page.slug}`

    }

  };

}



export default function SeoPage({ params }) {

  const page = getSeoPage(params.slug);

  if (!page) notFound();



  const relatedPages =

    page.relatedSlugs?.map((s) => getSeoPage(s)).filter(Boolean) ?? [];



  return (

    <main

      style={{

        padding: '40px 24px',

        maxWidth: 900,

        margin: '0 auto'

      }}

    >

      <h1 style={{ fontSize: '2.4rem', marginBottom: 20 }}>{page.h1}</h1>

      <p style={{ opacity: 0.9, lineHeight: '1.6' }}>{page.intro}</p>



      <h2 style={{ marginTop: 40 }}>What We Build</h2>

      <ul style={{ paddingLeft: 20, marginTop: 12 }}>

        {page.bullets.map((b) => (

          <li key={b} style={{ margin: '8px 0' }}>{b}</li>

        ))}

      </ul>



      {relatedPages.length > 0 && (

        <>

          <h2 style={{ marginTop: 40 }}>Related Services</h2>

          <ul style={{ paddingLeft: 20 }}>

            {relatedPages.map((rp) => (

              <li key={rp.slug}>

                <a href={`/seo-pages/${rp.slug}`}>{rp.h1}</a>

              </li>

            ))}

          </ul>

        </>

      )}



      <section

        style={{

          marginTop: 40,

          padding: 18,

          borderRadius: 10,

          backgroundColor: 'rgba(56,189,248,0.12)',

          border: '1px solid rgba(56,189,248,0.35)'

        }}

      >

        <h2 style={{ marginBottom: 8 }}>Start Your Project</h2>

        <p style={{ opacity: 0.9 }}>

          Text PJ at <strong>773-544-1231</strong> or email{' '}

          <a href="mailto:pj@sideguysolutions.com">pj@sideguysolutions.com</a>.

          Quick chat. Honest guidance. High-quality builds.

        </p>

      </section>

    </main>

  );

}

