const API_URL = "http://localhost:5001/api/products/";

async function fetchProducts() {
  const res = await fetch(API_URL);
  const json = await res.json();
  return json.data;
}

async function createProduct(data) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

async function updateProduct(id, data) {
  const res = await fetch(`${API_URL}${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

async function deleteProduct(id) {
  const res = await fetch(`${API_URL}${id}`, { method: "DELETE" });
  return await res.json();
}
