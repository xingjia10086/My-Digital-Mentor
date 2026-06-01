function Topbar({ content }) {
  const hrefFor = (id) => (id.startsWith("/") || id.startsWith("http") ? id : `#${id}`);

  return (
    <header className="topbar">
      <div className="shell topbar-inner">
        <div className="brand">
          <span className="brand-mark" />
          <span>{content.brand}</span>
        </div>
        <nav className="nav">
          {content.nav.map(([id, label]) => (
            <a key={id} href={hrefFor(id)}>
              {label}
            </a>
          ))}
          <LanguageSwitch locale={content.locale} switcher={content.switcher} />
        </nav>
      </div>
    </header>
  );
}

function LanguageSwitch({ locale, switcher }) {
  return (
    <div className="lang-switch">
      <a className={locale === "en" ? "active" : ""} href={switcher.en}>
        EN
      </a>
      <span>/</span>
      <a className={locale === "zh" ? "active" : ""} href={switcher.zh}>
        中文
      </a>
    </div>
  );
}

function Hero({ content }) {
  const { shared } = content;

  return (
    <section className="hero">
      <div className="shell hero-grid">
        <div className="hero-copy">
          <div className="eyebrow">{content.eyebrow}</div>
          <h1>{content.heroTitle}</h1>
          <p className="hero-subtitle">{content.heroSubtitle}</p>
          <div className="cta-row">
            <a className="button button-primary" href={content.primaryCta[1]}>
              {content.primaryCta[0]}
            </a>
            <a className="button button-secondary" href={content.secondaryCta[1]}>
              {content.secondaryCta[0]}
            </a>
          </div>
          <div className="proof-grid">
            {content.proofs.map(([title, body]) => (
              <div className="proof" key={title}>
                <strong>{title}</strong>
                <span>{body}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="hero-visual">
          <div className="visual-block">
            <div className="visual-tag">{content.visualTag}</div>
            <h3>{content.visualTitle}</h3>
            <p>{content.visualBody}</p>
          </div>
          <div className="visual-image">
            <img src={shared.screenshots.hero} alt="Personal AI Writer screenshot" />
          </div>
          <div className="visual-points">
            {content.points.map(([title, body]) => (
              <div className="point" key={title}>
                <strong>{title}</strong>
                <span>{body}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function SectionHeader({ kicker, title, copy }) {
  return (
    <div className="section-head">
      <div>
        <div className="section-kicker">{kicker}</div>
        <h2>{title}</h2>
      </div>
      <div className="section-copy">{copy}</div>
    </div>
  );
}

function CardsSection({ id, data, columns = "grid-2" }) {
  return (
    <section id={id}>
      <div className="shell">
        <SectionHeader kicker={data.kicker} title={data.title} copy={data.copy} />
        <div className={columns}>
          {data.cards.map(([title, body]) => (
            <article className="card" key={title}>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function ProcessSection({ data }) {
  return (
    <section id="how">
      <div className="shell">
        <SectionHeader kicker={data.kicker} title={data.title} copy={data.copy} />
        <div className="process-grid">
          {data.steps.map(([step, title, body]) => (
            <article className="card" key={title}>
              <div className="step-no">{step}</div>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function ComparisonSection({ data }) {
  return (
    <section id="difference">
      <div className="shell">
        <SectionHeader kicker={data.kicker} title={data.title} copy={data.copy} />
        <div className="compare-wrap">
          <table>
            <thead>
              <tr>
                {data.tableHead.map((cell) => (
                  <th key={cell}>{cell}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.rows.map((row) => (
                <tr key={row[0]}>
                  {row.map((cell) => (
                    <td key={cell}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

function ShowcaseSection({ data, screenshot }) {
  return (
    <section id="showcase">
      <div className="shell">
        <SectionHeader kicker={data.kicker} title={data.title} copy={data.copy} />
        <div className="showcase">
          <div className="showcase-copy">
            <h3>{data.bodyTitle}</h3>
            <p>{data.bodyCopy}</p>
            <div className="showcase-list">
              {data.items.map(([title, body]) => (
                <div className="showcase-item" key={title}>
                  <strong>{title}</strong>
                  <span>{body}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="showcase-image">
            <img src={screenshot} alt="Archive-powered showcase screenshot" />
          </div>
        </div>
      </div>
    </section>
  );
}

function FinalCta({ final }) {
  return (
    <section>
      <div className="shell">
        <div className="cta-panel">
          <div className="section-kicker">{final.kicker}</div>
          <h2>{final.title}</h2>
          <p>{final.body}</p>
          <div className="cta-row">
            <a className="button button-primary" href={final.primary[1]}>
              {final.primary[0]}
            </a>
            <a className="button button-secondary" href={final.secondary[1]}>
              {final.secondary[0]}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer({ footer }) {
  return (
    <footer className="footer">
      <div className="shell footer-inner">
        <div>{footer[0]}</div>
        <div>{footer[1]}</div>
      </div>
    </footer>
  );
}

export default function LandingPage({ content }) {
  return (
    <div className="site-shell">
      <Topbar content={content} />
      <Hero content={content} />
      <CardsSection id="problem" data={content.sections.problem} />
      <ProcessSection data={content.sections.how} />
      <ComparisonSection data={content.sections.difference} />
      <ShowcaseSection
        data={content.sections.showcase}
        screenshot={content.shared.screenshots.archive}
      />
      <CardsSection id="benefits" data={content.sections.benefits} columns="grid-2" />
      <CardsSection id="use-cases" data={content.sections.useCases} columns="grid-2" />
      <FinalCta final={content.final} />
      <Footer footer={content.footer} />
    </div>
  );
}
