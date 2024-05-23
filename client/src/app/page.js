"use client";
import Link from "next/link";
import { LampContainer } from "@/components/ui/lamp";
import { motion } from "framer-motion";
import {
  TypewriterEffect,
  TypewriterEffectSmooth,
} from "@/components/ui/typewriter-effect";

export default function Home() {
  const aboutWords = [
    { text: "The" },
    { text: "web" },
    { text: "application" },
    { text: "facilitates" },
    { text: "the" },
    { text: "scheduling" },
    { text: "of" },
    { text: "tasks" },
    { text: "on" },
    { text: "cloud" },
    { text: "datasets" },
    { text: "using" },
    { text: "two" },
    { text: "prominent" },
    { text: "machine" },
    { text: "learning" },
    { text: "algorithms:" },
    { text: "Logistic", className: "text-blue-500 dark:text-blue-500" },
    { text: "Regression", className: "text-blue-500 dark:text-blue-500" },
    { text: "and" },
    { text: "Decision", className: "text-blue-500 dark:text-blue-500" },
    { text: "Tree.", className: "text-blue-500 dark:text-blue-500" },
    { text: "These" },
    { text: "algorithms" },
    { text: "are" },
    { text: "employed" },
    { text: "to" },
    { text: "predict" },
    { text: "the" },
    { text: "availability" },
    { text: "of" },
    { text: "resources" },
    { text: "for" },
    { text: "scheduling" },
    { text: "tasks," },
    { text: "thus" },
    { text: "enabling" },
    { text: "users" },
    { text: "to" },
    { text: "make" },
    { text: "informed" },
    { text: "decisions" },
    { text: "regarding" },
    { text: "task" },
    { text: "allocation." },
    { text: "The" },
    { text: "application" },
    { text: "provides" },
    { text: "key" },
    { text: "performance" },
    { text: "metrics" },
    { text: "such" },
    { text: "as" },
    { text: "accuracy," },
    { text: "precision," },
    { text: "and" },
    { text: "F1" },
    { text: "score" },
    { text: "for" },
    { text: "both" },
    { text: "algorithms," },
    { text: "empowering" },
    { text: "users" },
    { text: "to" },
    { text: "evaluate" },
    { text: "their" },
    { text: "effectiveness" },
    { text: "in" },
    { text: "real-world" },
    { text: "scenarios." },
  ];

  const userFriendlyDesign = [
    { text: "User-Friendly" },
    { text: "Design:", className: "text-blue-500 dark:text-blue-500" },
    { text: "A" },
    { text: "sleek," },
    { text: "intuitive" },
    { text: "web" },
    { text: "application" },
    { text: "that" },
    { text: "simplifies" },
    { text: "complex" },
    { text: "machine" },
    { text: "learning" },
    { text: "operations." },
  ];

  const comprehensiveEvaluation = [
    { text: "Comprehensive" },
    { text: "Algorithmic" },
    { text: "Evaluation:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Employs" },
    { text: "the" },
    { text: "analytical" },
    { text: "strengths" },
    { text: "of" },
    { text: "Logistic" },
    { text: "Regression" },
    { text: "and" },
    { text: "Decision" },
    { text: "Tree" },
    { text: "algorithms" },
    { text: "for" },
    { text: "nuanced" },
    { text: "task" },
    { text: "scheduling" },
    { text: "insights." },
  ];

  const quantitativeMetrics = [
    { text: "Quantitative" },
    { text: "Metrics" },
    { text: "Display:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Showcases" },
    { text: "accuracy," },
    { text: "precision," },
    { text: "and" },
    { text: "F1" },
    { text: "score" },
    { text: "metrics," },
    { text: "enabling" },
    { text: "users" },
    { text: "to" },
    { text: "make" },
    { text: "informed" },
    { text: "decisions" },
    { text: "based" },
    { text: "on" },
    { text: "algorithm" },
    { text: "performance." },
  ];

  const predictiveResourceManagement = [
    { text: "Predictive" },
    { text: "Resource" },
    { text: "Management:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Offers" },
    { text: "reliable" },
    { text: "predictions" },
    { text: "on" },
    { text: "resource" },
    { text: "allocation," },
    { text: "facilitating" },
    { text: "smoother" },
    { text: "cloud" },
    { text: "operations." },
  ];

  const graphicalDataRepresentation = [
    { text: "Graphical" },
    { text: "Data" },
    { text: "Representation:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Provides" },
    { text: "bar" },
    { text: "graphs" },
    { text: "for" },
    { text: "immediate" },
    { text: "visual" },
    { text: "comparison" },
    { text: "of" },
    { text: "algorithm" },
    { text: "outcomes." },
    { text: "Cloud" },
    { text: "Dataset" },
    { text: "Specialization:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Tailored" },
    { text: "specifically" },
    { text: "for" },
    { text: "cloud" },
    { text: "computing" },
    { text: "datasets" },
    { text: "to" },
    { text: "ensure" },
    { text: "maximum" },
    { text: "relevance" },
    { text: "and" },
    { text: "efficiency." },
  ];

  const maximizedModelPotential = [
    { text: "Maximized" },
    { text: "Model" },
    { text: "Potential:", className: "text-blue-500 dark:text-blue-500" },
    { text: "Enables" },
    { text: "users" },
    { text: "to" },
    { text: "leverage" },
    { text: "the" },
    { text: "full" },
    { text: "capabilities" },
    { text: "of" },
    { text: "the" },
    { text: "machine" },
    { text: "learning" },
    { text: "model" },
    { text: "for" },
    { text: "superior" },
    { text: "cloud" },
    { text: "resource" },
    { text: "scheduling." },
  ];

  return (
    <main className="flex items-center justify-center p-20 flex-col">
      <LampContainer id="about">
        <motion.h1
          initial={{ opacity: 0.5, y: 100 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="mt-8 bg-gradient-to-br from-slate-300 to-slate-500 py-4 bg-clip-text text-center text-5xl font-medium tracking-tight text-transparent md:text-8xl"
        >
          About The Project
        </motion.h1>
      </LampContainer>
      {/* <TypewriterEffect
        words={[
          {
            text: "Abstract",
            className: "text-blue-500 dark:text-blue-500 text-2xl md:text-2xl",
          },
        ]}
      /> */}
      <TypewriterEffect
        words={userFriendlyDesign.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1"
      />
      <TypewriterEffect
        words={comprehensiveEvaluation.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1"
      />
      <TypewriterEffect
        words={quantitativeMetrics.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1"
      />
      <TypewriterEffect
        words={predictiveResourceManagement.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1"
      />
      <TypewriterEffect
        words={graphicalDataRepresentation.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1 "
      />
      <TypewriterEffect
        words={maximizedModelPotential.map((word) => ({
          ...word,
          className: word.className
            ? `${word.className} text-2xl md:text-2xl`
            : "text-2xl md:text-2xl",
        }))}
        className="mb-1"
      />
    </main>
  );
}
