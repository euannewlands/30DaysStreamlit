# 30DaysStreamlit
Following challenges given on https://30days.streamlit.app/

Learning Log
---
Below is an explict list of moments I found to be noteable learning experiences during completion of the 30 Days of Streamlit "challenge"
- **Day 4:** I'm not sure if I've ever spent time formatting the output of DataFrames using Pandas Styler object, that was useful.
- **Day 4:** I'd never used the `plotly` package before - I was familiar with `matplotlib`, from university coding, and I had some knowledge about `seaborn`, from some earlier Data Engineering projects.
- **Day 9:** I took the time to plot some life expectancy data using the `altair` package, which was new to me
- **Day 14:** I didn't previously know about Streamlit Components, community built extensions to Streamlit. Now I do!
---

Below is a log of actions related to the instruction in each "daily challenge".
---
### Day 1: Setup
- created an environment `stenv`, to install the streamlit library
- opened up the demo and bookmarked all the relevant streamlit urls (docs, what's new?)

### Day 2: Building First Streamlit
- created the `Hello World!` streamlit app equivalent

### Day 3: st.button
- used st.button to introduce the option of conditions on the streamlit app

### Day 4: Mock Data Science Portfolio
- Followed [Ken Jee's video](https://www.youtube.com/watch?v=Yk-unX4KnV4) to build up a dashboard to gain insights into his YouTube video performance
- Data from Kaggle can be [found here](https://www.kaggle.com/datasets/kenjee/ken-jee-youtube-data)
- Basic feature engineering using `pandas`
- Fiddly formatting of DataFrames
- Plotly bar and scatter charts

### Day 5: st.write
- investigated th variability of st.write, where the output format is dependent on the input object

### Day 6-7: deploy to Streamlit Community Cloud
- The challenge took me through steps on how to deploy public apps to the community cloud

### Day 8 st.slider
- Added a slider for continuous values - I investigated how the step parameter worked for a datetime slider using a datetime.timedelta object

### Day 9: st.line_chart
- use st.line_chart to see how streamlit makes it easy to 'just plot this'
- explored plotting configurations with `altair` plotting

### Day 10: st.selectbox
- messed about with the various configurations of st.selecbox

### Day 11: st.multiselect
- messed about with the various configurations of st.multiselect

### Day 12: st.checkbox
- messed about with the various configurations of st.checkbox

### Day 14: Streamlit Components
- learnt about streamlit components, and where to find more!
- ran the common ydata_profiling and presented the results in streamlit

### Day 15: st.latex
- I learn Streamlit supports Latex code. I included a formular I used in one of my Astrophysics projects at university