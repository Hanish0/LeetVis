# LeetCode Video Generator

A web application that generates AI-powered video explanations for LeetCode problems. Users can enter a problem title, select a programming language, and choose from different explanation types to get customized video tutorials.

## Features

- **Problem Input**: Enter any LeetCode problem title
- **Language Selection**: Choose from Python, Java, or C++
- **Video Types**: Generate different types of explanations:
  - Problem Explanation
  - Brute Force Solution
  - Optimal Solution
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) to view the application

### Building for Production

```bash
npm run build
npm start
```

## Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to [Vercel](https://vercel.com)
3. Vercel will automatically deploy your application

The application is optimized for static deployment and will work seamlessly on Vercel's platform.

## Tech Stack

- **Frontend**: Next.js 15 with React 19
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript
- **Deployment**: Vercel

## Project Structure

```
src/
├── app/
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Main page component
```

## Contributing

This project is part of a larger system that will include backend video generation capabilities. The frontend is designed to be ready for integration with the backend API.
