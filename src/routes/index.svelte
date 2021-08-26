<script context="module">
  export async function load({ fetch }) {
      const res = await fetch('/index.json');
      if (res.ok) {
          return {
              props: {
                  data: await res.json(),
              },
          };
      }
      return {
          status: res.status,
          error: new Error("Could not load"),
      };
  }
</script>

<script>
  export let data;
  console.log(data);
  let nf = Intl.NumberFormat("cs");
  let df = Intl.DateTimeFormat("cs", {day: 'numeric', month: 'numeric', year: 'numeric'})
  let options = { year: 'numeric', month: 'numeric', day: 'numeric' };
</script>

<h1 class="question">Je očkování bezpečné?</h1>
<p class="answer">Ano.</p>
<div class="comparison">
  <section class="vaccine">
    <h2>
      <img src="/img/vaccine.svg" alt="vakcína" />
      Vakcína
      <span>proti COVID-19</span>
    </h2>
    <p class="count vaccinated">{nf.format(data.vaccines.second_vaccines)}</p>
    <h3>očkovaných</h3>
    <p class="count vaccine-deaths">0</p>
    <h3 class="vaccine-deaths">zemřelých</h3>
  </section>
  <section class="virus">
    <h2>
      <img src="/img/virus.svg" alt="koronavirus" />
      COVID-19
      <span>onemocnění</span>
    </h2>
    <p class="count covid-infected">{nf.format(data.stats.cases)}</p>
    <h3 class="covid-infected">nakažených</h3>
    <p class="count covid-deaths">{nf.format(data.stats.deaths)}</p>
    <h3 class="covid-deaths">zemřelých</h3>
  </section>
</div>
<p class="period">
  Data pro Česko za období od začátku pandemie do&nbsp;<time>{df.format(data.date)}</time>.
</p>
<p><b>Data hovoří jasně.</b> Očkování proti COVID-19 je skutečně bezpečné. Pouze někteří z nás projdou mírnými nežádoucími účinky.</p>
<p>Očkování je naše <b>nejúčinnější zbraň</b> v boji proti pandemii koronaviru. Čím více lidí je očkováno, tím rychleji se vracíme k běžnému životu.</p>
<p class="faq">
  <a href="https://www.iniciativa-snih.cz/nejcastejsi-dotazy-kolem-ockovani/">
    Chci vědět víc
  </a>
</p>
