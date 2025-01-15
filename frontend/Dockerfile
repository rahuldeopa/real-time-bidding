# Use the official Node.js image from the DockerHub
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy the frontend code into the container
COPY ./src /app/src
COPY ./public /app/public
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

# Install dependencies
RUN npm install

# Expose the port the app runs on
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
