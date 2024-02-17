import streamlit as st
import pandas as pd
import numpy as np

# st.header('Line chart')

# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])

# st.line_chart(chart_data)

##################################


### Extension of challenge for own learning ###
from vega_datasets import data
import altair as alt

source_df = data.countries()

afghan_swiss_uk_df = source_df.loc[source_df['country'].isin(
    ('Afghanistan','Switzerland','United Kingdom','Japan','Rwanda')
)]

afghan_swiss_uk_df = afghan_swiss_uk_df.loc[:,['year', 'life_expect', 'country']]

c = (
   alt.Chart(afghan_swiss_uk_df)
   .mark_line()
   .encode(
    x="year", y="life_expect", size="country", color="country", tooltip=[
        "year", "life_expect", "country"
    ], strokeDash='country'
))

st.altair_chart(c, use_container_width=True,theme='streamlit')


base = alt.Chart(source_df).encode(
    alt.X("life_expect:Q")
        .scale(zero=False)
        .title("Life Expectancy (years)"),
    alt.Y("country:N")
        .axis(offset=5, ticks=False, minExtent=70, domain=False)
        .title("Country")
).transform_filter(
    alt.FieldOneOfPredicate(field="country", oneOf=('Afghanistan','Switzerland','United Kingdom','Japan','Rwanda'))
).transform_filter(
    alt.FieldOneOfPredicate(field='year', oneOf=[1955, 2000])
)


line = base.mark_line().encode(
    detail="country",
    color=alt.value("#db646f")
).transform_filter(
    alt.FieldOneOfPredicate(field="year", oneOf=[1955, 2000])
)

point = base.mark_point(filled=True).encode(
    alt.Color("year").scale(range=["#e6959c", "#911a24"], domain=[1955, 2000]),
    size=alt.value(100),
    opacity=alt.value(1),
)

st.altair_chart(line+point, use_container_width=True,theme='streamlit')