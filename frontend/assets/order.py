# MARU order menu (PyScript, MicroPython runtime). Loaded by index.html.
# Change PRICE here; also update the "₱49" text in index.html.
from pyscript import document, window, when

PRICE = 49
MAX_QTY = 50
PESO = "\u20b1"
ITEM = "Ham & Cheese Takoyaki"

def el(i):
    return document.getElementById(i)

def peso(n):
    s = str(n)
    out = ""
    while len(s) > 3:
        out = "," + s[-3:] + out
        s = s[:-3]
    return PESO + s + out

def read_qty():
    try:
        n = int(el("qty").value)
    except Exception:
        return 0
    if n < 1:
        return 0
    return min(n, MAX_QTY)

def render(event=None):
    q = read_qty()
    if q:
        el("sum-line").textContent = str(q) + " \u00d7 " + ITEM
    else:
        el("sum-line").textContent = "Enter a quantity from 1 to " + str(MAX_QTY)
    el("sum-total").textContent = peso(q * PRICE)
    el("qty-minus").disabled = q <= 1
    el("qty-plus").disabled = q >= MAX_QTY
    el("err").hidden = True

def step(d):
    q = read_qty() or 1
    q = max(1, min(MAX_QTY, q + d))
    el("qty").value = str(q)
    render()

@when("click", "#qty-minus")
def minus(event):
    step(-1)

@when("click", "#qty-plus")
def plus(event):
    step(1)

@when("input", "#qty")
def typing(event):
    render()

@when("change", "#qty")
def settle(event):
    el("qty").value = str(read_qty() or 1)
    render()

def fail(msg, field):
    el("err").textContent = msg
    el("err").hidden = False
    el(field).focus()

@when("submit", "#order-form")
def place(event):
    q = read_qty()
    name = str(el("cust").value).strip()
    if q < 1:
        fail("Enter a quantity from 1 to " + str(MAX_QTY) + ".", "qty")
        return
    if not name:
        fail("Add your name so we know whose order it is.", "cust")
        return
    mode = "Delivery" if el("mode-delivery").checked else "Pick-up"
    lines = [
        "Hi MARU! I'd like to order:",
        "",
        str(q) + " x " + ITEM + " - " + peso(q * PRICE),
        "Name: " + name,
        "Option: " + mode,
    ]
    el("order-text").value = "\n".join(lines)
    el("copied").textContent = ""
    el("order-edit").hidden = True
    el("order-done").hidden = False
    el("order-done").focus()

@when("click", "#copy")
def copy_order(event):
    box = el("order-text")
    box.focus()
    box.select()
    ok = False
    try:
        ok = bool(document.execCommand("copy"))
    except Exception:
        ok = False
    if not ok:
        try:
            window.navigator.clipboard.writeText(box.value)
            ok = True
        except Exception:
            ok = False
    if ok:
        el("copied").textContent = "Copied! Now paste it in Messenger."
    else:
        el("copied").textContent = "Press Ctrl+C (or \u2318C) to copy the selected text."

@when("click", "#msg-open")
def open_messenger(event):
    copy_order(event)

@when("click", "#edit")
def edit(event):
    el("order-done").hidden = True
    el("order-edit").hidden = False
    el("qty").focus()

# Orders go to the same link as the "Message Us to Order" button.
el("msg-open").href = str(el("contact-btn").href)
el("place").disabled = False
el("place").textContent = "Place order"
document.body.setAttribute("data-ready", "1")
render()
