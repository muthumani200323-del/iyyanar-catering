from pathlib import Path
p = Path(r"c:\Users\8121c\Downloads\iyyanar_catering\iyyanar_catering\iyyanar_catering\templates\index.html")
text = p.read_text(encoding='utf-8')
old = '''          {% if review_count %}
          <div class="rev-summary">
            <span class="rev-avg">{{ review_avg }}</span>
            <span class="stars" aria-label="{{ review_avg }} out of 5 stars">{% for i in "12345" %}<span>★</span>{%
              endfor %}</span>
            <span>from {{ review_count }} review{{ review_count|pluralize }}</span>
          </div>
          {% endif %}

          {% if user.is_staff and pending %}
          <div class="rev-list" style="margin-bottom:1rem">
            <span class="badge">Admin only · waiting for approval</span>
            {% for r in pending %}
            <article class="rev" style="border-style:dashed">
              <span class="stars" aria-label="{{ r.rating }} out of 5 stars">{% for i in "12345" %}{% if forloop.counter
                <= r.rating %}<span>★
              </span>{% else %}<span class="off">★</span>{% endif %}{% endfor %}</span>
              <span class="who">{{ r.name|default:"Customer" }}</span>
              <span class="meta">{% if r.place %}{{ r.place }} · {% endif %}{{ r.created|date:"d M Y" }}</span>
              <p>{{ r.text }}</p>
              <div class="del-row">
                <form class="inline-form" method="post" action="{% url 'catering:review_approve' r.pk %}">{% csrf_token
                  %}<button class="btn-sm" type="submit">Approve</button></form>
                <form class="inline-form" method="post" action="{% url 'catering:review_delete' r.pk %}"
                  data-confirm="Delete this review?">{% csrf_token %}<button class="btn-sm danger"
                    type="submit">Delete</button></form>
              </div>
            </article>
            {% endfor %}
          </div>
          {% endif %}

          <div class="rev-list">
            {% for r in reviews %}
            <article class="rev">
              <span class="stars" aria-label="{{ r.rating }} out of 5 stars">{% for i in "12345" %}{% if forloop.counter
                <= r.rating %}<span>★
              </span>{% else %}<span class="off">★</span>{% endif %}{% endfor %}</span>
              <span class="who">{{ r.name|default:"Customer" }}</span>
              <span class="meta">{% if r.place %}{{ r.place }} · {% endif %}{{ r.created|date:"M Y" }}</span>
              <p>{{ r.text }}</p>
              {% if user.is_staff %}
              <div class="del-row">
                <form class="inline-form" method="post" action="{% url 'catering:review_delete' r.pk %}"
                  data-confirm="Delete this review?">{% csrf_token %}<button class="btn-sm danger"
                    type="submit">Delete</button></form>
              </div>
              {% endif %}
            </article>
            {% empty %}
            <div class="rev-empty"><strong>முதல் மதிப்புரையை நீங்கள் எழுதுங்கள்</strong>No reviews here yet. Be the
              first to share how your function went.</div>
            {% endfor %}
          </div>
'''
new = '''          {% if review_count %}
          <div class="rev-summary">
            <span class="rev-avg">{{ review_avg }}</span>
            <span class="stars" aria-label="{{ review_avg }} out of 5 stars">{% for i in "12345" %}<span>★</span>{% endfor %}</span>
            <span>from {{ review_count }} review{{ review_count|pluralize }}</span>
          </div>
          {% endif %}

          {% if user.is_staff and pending %}
          <div class="rev-list" style="margin-bottom:1rem">
            <span class="badge">Admin only · waiting for approval</span>
            {% for r in pending %}
            <article class="rev" style="border-style:dashed">
              <span class="stars" aria-label="{{ r.rating }} out of 5 stars">{% for i in "12345" %}{% if forloop.counter <= r.rating %}<span>★</span>{% else %}<span class="off">★</span>{% endif %}{% endfor %}</span>
              <span class="who">{{ r.name|default:"Customer" }}</span>
              <span class="meta">{% if r.place %}{{ r.place }} · {% endif %}{{ r.created|date:"d M Y" }}</span>
              <p>{{ r.text }}</p>
              <div class="del-row">
                <form class="inline-form" method="post" action="{% url 'catering:review_approve' r.pk %}">{% csrf_token %}<button class="btn-sm" type="submit">Approve</button></form>
                <form class="inline-form" method="post" action="{% url 'catering:review_delete' r.pk %}" data-confirm="Delete this review?">{% csrf_token %}<button class="btn-sm danger" type="submit">Delete</button></form>
              </div>
            </article>
            {% endfor %}
          </div>
          {% endif %}

          <div class="rev-list">
            {% for r in reviews %}
            <article class="rev">
              <span class="stars" aria-label="{{ r.rating }} out of 5 stars">{% for i in "12345" %}{% if forloop.counter <= r.rating %}<span>★</span>{% else %}<span class="off">★</span>{% endif %}{% endfor %}</span>
              <span class="who">{{ r.name|default:"Customer" }}</span>
              <span class="meta">{% if r.place %}{{ r.place }} · {% endif %}{{ r.created|date:"M Y" }}</span>
              <p>{{ r.text }}</p>
              {% if user.is_staff %}
              <div class="del-row">
                <form class="inline-form" method="post" action="{% url 'catering:review_delete' r.pk %}" data-confirm="Delete this review?">{% csrf_token %}<button class="btn-sm danger" type="submit">Delete</button></form>
              </div>
              {% endif %}
            </article>
            {% empty %}
            <div class="rev-empty"><strong>Be the first to review</strong> No reviews here yet. Be the first to share how your function went.</div>
            {% endfor %}
          </div>
'''
if old not in text:
    raise SystemExit('Old block not found, current text was:\n' + text[text.find('    {% if review_count %}'):text.find('      <form class="card" id="revform"')])
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
print('done')
print(repr(p.read_text(encoding='utf-8')[text.find('    {% if review_count %}'):text.find('      <form class="card" id="revform"')]))
