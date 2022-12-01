# Options

## Write-Up

Whe openning the challenge via this link : http://devfest22-cybersec.gdgalgiers.com:1600/

you will get a page where you will find a form with a select options.

```html
<html lang="en"><head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant</title>
  </head>
  <body>
    <form id="form">
      <label for="options">Choose an option :</label>
      <select name="options" id="options">
        <option value="pizza">Pizza</option>
        <option value="cheeseburger">Cheese burger</option>
        <option value="frenchfries">French fries</option>
        <option value="tacos">Tacos</option>
      </select>
      <input type="submit" value="submit">
    </form>
    <script>
      const form = document.getElementById("form");
      const options = document.getElementById("options");
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        window.location.href = `${window.location.origin}/${options.value}`
      });
    </script>
  
</body></html>
```

You can see that the form submission is actually a redirection to another route, and from the description of the challenge : `Do you have all the options ?`, we can deduce that the idea is to find the missing route.

To do that, we can use the `OPTIONS` method (a related method to the challenge), that may help us and indeed, it gives us the list of all available options :

```
curl 'http://devfest22-cybersec.gdgalgiers.com:1600/' -X OPTIONS
```

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Restaurant</title>
  </head>
  <body>
    <ul>
        <li>Pizza</li>
        <li>Cheese burger</li>
        <li>French fries</li>
        <li>Tacos</li>
        <li>Karantika</li>
    </ul>
  </body>
</html>
```

After that, we need to target the `/karantika` option to see what it is in ther, it is will give us the following json object : 

```json
{"URL":"https://dpaste.org/pZATZ/raw"}
```

After redirecting to that website, a base64 string will be send :

```
RGV2RmVzdDIye0l0NV80bGxfNEIwdVRfMHBUMTBuNX0=
```

All we have to do is to decode it :

```
echo "RGV2RmVzdDIye0l0NV80bGxfNEIwdVRfMHBUMTBuNX0=" | base64 -d
```

It will give us the flag :

```
DevFest22{It5_4ll_4B0uT_0pT10n5}
```


## Flag

DevFest22{It5_4ll_4B0uT_0pT10n5} 

## More Information

 - HTTP Methods and Messages : https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages