// Select tab functionality
function selectTab(element) {
     const allTabs = document.querySelectorAll('.tab-item');
     allTabs.forEach(tab => {
          tab.classList.remove('active');
     });

     element.classList.add('active');
}

// Profile dropdown toggle
function toggleProfile() {
     document.getElementById("profileDropdown").classList.toggle("show");
}

// stock search
const input = document.getElementById("searchInput");
const resultsBox = document.getElementById("searchResults");

if (input) {
     input.addEventListener("input", async function () {
          const query = this.value.trim();
          resultsBox.innerHTML = "";

          if (!query) {
               resultsBox.style.display = "none";
               return;
          }

          try {
               const res = await fetch(`/stocks/search?q=${query}`);
               const stocks = await res.json();

               if (stocks.length === 0) {
                    resultsBox.innerHTML =
                         `<div class="search-item disabled">No stocks found</div>`;
                    resultsBox.style.display = "block";
                    return;
               }

               stocks.forEach(stock => {
                    const div = document.createElement("div");
                    div.className = "search-item";
                    div.textContent = `${stock.name}`;

                    div.onclick = () => {
                         resultsBox.style.display = "none";
                         input.value = "";
                         window.location.href = `/stocks/${stock.token}`;
                    };

                    resultsBox.appendChild(div);
               });

               resultsBox.style.display = "block";

          } catch (err) {
               console.error("Search error:", err);
               resultsBox.style.display = "none";
          }
     });
}


// holding auto load
document.addEventListener("DOMContentLoaded", () => {
     loadUserHoldings();
});

function loadUserHoldings() {
     fetch("/holding/order", {
          method: "POST",
          headers: {
               "Content-Type": "application/json"
          }
     })
          .then(res => res.json())
          .then(data => {
               if (data.error) {
                    console.error(data.error);
                    return;
               }

               renderHoldings(data.holdings);
          })
          .catch(err => console.error("Holdings error:", err));
}

function renderHoldings(holdings) {
     const container = document.getElementById("holding-body");
     container.innerHTML = "";

     const symbols = Object.keys(holdings);

     if (symbols.length === 0) {
          container.innerHTML =
               `<div class="holding-row">No holdings</div>`;
          
          console.log("No holdings to display");
          return;
     }

     console.log("holdings to display");

     symbols.forEach(symbol => {
          const h = holdings[symbol];

          // basic calculations
          const market_price = h.market_price || h.avg_buy_price;
          const current_value = (market_price * h.quantity).toFixed(2);
          const invested_value = (h.avg_buy_price * h.quantity).toFixed(2);
          const profit_loss = (current_value - invested_value).toFixed(2);
          const return_percent = ((profit_loss / invested_value) * 100).toFixed(2);


          const row =
               ` <div class="holding-row">
               <div>
                    <strong>${symbol}</strong>
                    <p>${h.quantity} shares · Avg. ₹${h.avg_buy_price}</p>
               </div>
               <div>
                    ₹${market_price}
                    <p style="color:${return_percent >= 0 ? '#04b488' : '#ff4d4f'};">
                         ${return_percent >= 0 ? '+' : ''}${return_percent}%
                    </p>
               </div>
               <div style="color:${return_percent >= 0 ? '#04b488' : '#ff4d4f'};">
                    ${profit_loss >= 0 ? '+' : ''}₹${profit_loss}
                    <p>${return_percent}%</p>
               </div>
               <div>
                    ₹${current_value}
                    <p>₹${invested_value}</p>
               </div>
          </div> `;

          container.innerHTML += row;
     });
}