// frontend/webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const dotenv = require('dotenv');
const fs = require('fs');

// Load environment variables from .env file
const envFilePath = path.resolve(__dirname, '.env');
const fileEnv = fs.existsSync(envFilePath) ? dotenv.config({ path: envFilePath }).parsed : {};

// Reduce environment variables to key-value pairs for DefinePlugin
const envKeys = fileEnv
  ? Object.keys(fileEnv).reduce((prev, next) => {
      prev[`process.env.${next}`] = JSON.stringify(fileEnv[next]);
      return prev;
    }, {})
  : {};

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  devServer: {
    static: './dist',
    historyApiFallback: true,
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5001' // Proxy API requests to backend
    }
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/, // If you're using CSS
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i, // If you're using images
        type: 'asset/resource',
      },
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html' // Ensure this path is correct
    }),
    new webpack.DefinePlugin(envKeys), // Define environment variables
  ]
};
