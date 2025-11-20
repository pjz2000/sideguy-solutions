import { getAllSeoSlugs, getSeoPage } from "../../../lib/seoPages";



export function generateStaticParams() {

  return getAllSeoSlugs().map((slug) => ({ slug }));

}



export default function SeoPage({ params }) {

  const page = getSeoPage(params.slug);



  if (!page) {

    return (

      <div style={{ padding: "40px", color: "white" }}>

        <h1>Page Not Found</h1>

      </div>

    );

  }



  return (

    <div style={{ padding: "40px", maxWidth: "900px", margin: "0 auto", color: "white" }}>

      <h1>{page.h1}</h1>

      <p style={{ opacity: 0.8, marginTop: "20px" }}>{page.intro}</p>



      <h2 style={{ marginTop: "40px" }}>What We Offer</h2>

      <ul style={{ marginTop: "20px" }}>

        {page.bullets.map((b, i) => (

          <li key={i} style={{ marginBottom: "8px" }}>{b}</li>

        ))}

      </ul>



      <h2 style={{ marginTop: "40px" }}>Related Pages</h2>

      <ul style={{ marginTop: "20px" }}>

        {page.relatedSlugs.map((slug, i) => (

          <li key={i}>

            <a href={`/seo-pages/${slug}`} style={{ color: "#38bdf8" }}>

              {slug.replace(/-/g, " ")}

            </a>

          </li>

        ))}

      </ul>

    </div>

  );

}


