import React, { useEffect, useRef } from "react";
import Plotly from 'plotly.js-dist';

const PlotComponent = ({ figure }: { figure: any }) => {
  const plotRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (plotRef.current && figure) {
      const parsedFigure = JSON.parse(figure); // Parse if needed
      Plotly.newPlot(plotRef.current, parsedFigure.data, parsedFigure.layout, { responsive: true });
    }
  }, [figure]);

  return <div ref={plotRef} className="w-full h-[400px]"></div>;
};

export default PlotComponent;
